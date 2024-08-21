import React, { useState, useEffect, useMemo } from 'react';
import { useTable, useGlobalFilter, useSortBy, usePagination } from 'react-table';
import axios from 'axios';
import './App.css';

function GlobalFilter({
  preGlobalFilteredRows,
  globalFilter,
  setGlobalFilter,
}) {
  const count = preGlobalFilteredRows.length;

  return (
    <span className="dataTables_filter">
      Search:{' '}
      <input
        value={globalFilter || ''}
        onChange={e => {
          setGlobalFilter(e.target.value || undefined);
        }}
        placeholder={`${count} records...`}
        style={{
          fontSize: '1.1rem',
          border: '1px solid #ddd',
          borderRadius: '4px',
          padding: '5px 10px',
          marginLeft: '5px',
          width: '200px',
        }}
      />
    </span>
  );
}

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuthAndFetchData();
  }, []);

  const checkAuthAndFetchData = async () => {
    try {
      const authResponse = await axios.get('http://localhost:5000/api/check-auth', { withCredentials: true });
      if (authResponse.data.authenticated) {
        fetchLeaderboard();
      } else {
        window.location.href = 'http://localhost:5000/login';
      }
    } catch (error) {
      console.error('Error checking authentication:', error);
      setError('An error occurred while checking authentication. Please try again later.');
      setLoading(false);
    }
  };

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/leaderboard', { withCredentials: true });
      setData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
      setError('An error occurred while fetching the leaderboard. Please try again later.');
      setLoading(false);
    }
  };

  const columns = useMemo(
    () => [
      { Header: 'Rank', accessor: 'rank' },
      { Header: 'Athlete', accessor: 'athlete' },
      { Header: 'Total Distance (miles)', accessor: 'totalDistance' },
      { Header: 'Avg Distance (miles)', accessor: 'averageDistance' },
      {
        Header: 'Total Moving Time',
        accessor: 'totalMovingTime',
        Cell: ({ value }) => secondsToHMS(value),
      },
      {
        Header: 'Total Elapsed Time',
        accessor: 'totalElapsedTime',
        Cell: ({ value }) => secondsToHMS(value),
      },
      { Header: 'Total Elevation Gain (feet)', accessor: 'totalElevationGain' },
      { Header: 'Number of Activities', accessor: 'activityCount' },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    page,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize, globalFilter },
    preGlobalFilteredRows,
    setGlobalFilter,
  } = useTable(
    {
      columns,
      data,
      initialState: { pageIndex: 0, pageSize: 25 },
    },
    useGlobalFilter,
    useSortBy,
    usePagination
  );

  const secondsToHMS = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  const exportCSV = () => {
    window.location.href = 'http://localhost:5000/api/export_csv';
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="App">
      <h1>Strava Club Leaderboard</h1>
      <div className="table-controls">
        <button onClick={exportCSV} className="export-btn">
          Export to CSV
        </button>
        <GlobalFilter
          preGlobalFilteredRows={preGlobalFilteredRows}
          globalFilter={globalFilter}
          setGlobalFilter={setGlobalFilter}
        />
      </div>
      <div className="table-container">
        <table className="leaderboard" {...getTableProps()}>
          <thead>
            {headerGroups.map(headerGroup => {
              const { key, ...headerGroupProps } = headerGroup.getHeaderGroupProps();
              return (
                <tr key={key} {...headerGroupProps}>
                  {headerGroup.headers.map(column => {
                    const { key, ...columnProps } = column.getHeaderProps(column.getSortByToggleProps());
                    return (
                      <th key={key} {...columnProps}>
                        {column.render('Header')}
                        <span>
                          {column.isSorted
                            ? column.isSortedDesc
                              ? ' 🔽'
                              : ' 🔼'
                            : ''}
                        </span>
                      </th>
                    );
                  })}
                </tr>
              );
            })}
          </thead>
          <tbody {...getTableBodyProps()}>
            {page.map(row => {
              prepareRow(row);
              const { key, ...rowProps } = row.getRowProps();
              return (
                <tr key={key} {...rowProps}>
                  {row.cells.map(cell => {
                    const { key, ...cellProps } = cell.getCellProps();
                    return (
                      <td key={key} {...cellProps}>
                        {cell.render('Cell')}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <div className="pagination">
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {'<'}
        </button>{' '}
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {'>>'}
        </button>{' '}
        <span>
          Page{' '}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type="number"
            defaultValue={pageIndex + 1}
            onChange={e => {
              const page = e.target.value ? Number(e.target.value) - 1 : 0
              gotoPage(page)
            }}
            style={{ width: '100px' }}
          />
        </span>{' '}
        <select
          value={pageSize}
          onChange={e => {
            setPageSize(Number(e.target.value))
          }}
        >
          {[10, 25, 50].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default App;
import { useQueryParams } from '../hooks/useQueryParams';

interface FilterParams extends Record<string, string> {
  search: string;
  status: string;
  sortBy: string;
}

export default function Home() {
  const { getParam, setParam, getAllParams } = useQueryParams<FilterParams>();
  
  const search = getParam('search');
  const status = getParam('status');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setParam('search', e.target.value);
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setParam('status', e.target.value);
  };

  return (
    <div>
      <h1>Conference List</h1>
      <p>Welcome to ConfRadar - Your conference deadline tracker</p>
      
      <div style={{ marginTop: '2rem', marginBottom: '2rem' }}>
        <h3>Filters (demo of URL query params):</h3>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <input
            type="text"
            placeholder="Search conferences..."
            value={search || ''}
            onChange={handleSearchChange}
            style={{ padding: '0.5rem', flex: 1 }}
          />
          <select 
            value={status || ''} 
            onChange={handleStatusChange}
            style={{ padding: '0.5rem' }}
          >
            <option value="">All Status</option>
            <option value="upcoming">Upcoming</option>
            <option value="past">Past</option>
          </select>
        </div>
        <div style={{ marginTop: '1rem', color: '#888' }}>
          <small>Current filters: {JSON.stringify(getAllParams())}</small>
        </div>
      </div>
      
      {/* Conference list will be implemented here */}
      <p style={{ color: '#888' }}>Conference data will be loaded from the API...</p>
    </div>
  );
}


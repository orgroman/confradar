import { useParams } from 'react-router-dom';

export default function ConferenceDetail() {
  const { id } = useParams<{ id: string }>();
  
  return (
    <div>
      <h1>Conference Details</h1>
      <p>Conference ID: {id}</p>
      {/* Conference details will be implemented here */}
    </div>
  );
}

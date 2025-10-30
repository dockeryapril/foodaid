'use client';
export default function ResultList({ rows }:{ rows:any[] }){
  return (
    <div className="list">
      {rows.map(r => (
        <div key={r.id} className="card">
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
            <strong>{r.city ? `${r.city}, ${r.state||''}` : 'Unknown location'}</strong>
            {r.verified ? <span className="badge">Verified</span> : null}
          </div>
          <div style={{fontSize:12,opacity:0.8}}>{r.event_date_start ? new Date(r.event_date_start).toLocaleString() : 'No date'}</div>
          <p style={{whiteSpace:'pre-wrap'}}>{(r.description||'').slice(0,320)}{(r.description||'').length>320?'…':''}</p>
        </div>
      ))}
    </div>
  );
}

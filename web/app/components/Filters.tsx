'use client';
import { useState } from 'react';

export default function Filters({ onState, onCity, onVerified }:{ onState:(v:string)=>void, onCity:(v:string)=>void, onVerified:(v:boolean)=>void}){
  const [state, setState] = useState('');
  const [city, setCity] = useState('');
  const [ver, setVer] = useState(false);

  return (
    <div className="filters">
      <input placeholder="State (e.g., GA, MI)" value={state} onChange={e=>{ setState(e.target.value); onState(e.target.value); }} />
      <input placeholder="City (e.g., Atlanta, Grand Rapids)" value={city} onChange={e=>{ setCity(e.target.value); onCity(e.target.value); }} />
      <label style={{display:'flex',alignItems:'center',gap:6}}>
        <input type="checkbox" checked={ver} onChange={e=>{ setVer(e.target.checked); onVerified(e.target.checked); }} />
        Only verified
      </label>
    </div>
  );
}

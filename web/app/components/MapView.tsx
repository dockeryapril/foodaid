'use client';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

type Row = {
  id:number; description:string|null; city:string|null; state:string|null;
  latitude:number|null; longitude:number|null; event_date_start:string|null; verified:boolean|null;
};

export default function MapView({ rows }:{ rows: Row[] }){
  const center:[number, number] = [33.749, -84.388]; // Atlanta default
  const pts = rows.filter(r => r.latitude && r.longitude);
  return (
    <div className="map">
      <MapContainer center={center} zoom={6} style={{height:'100%', width:'100%'}}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {pts.map(p => (
          <Marker key={p.id} position={[p.latitude as number, p.longitude as number]}>
            <Popup>
              <strong>{p.city}, {p.state}</strong><br/>
              {p.event_date_start ? new Date(p.event_date_start).toLocaleString() : 'No date'}<br/>
              <small>{(p.description||'').slice(0,160)}{(p.description||'').length>160?'…':''}</small><br/>
              {p.verified ? <span className="badge">Verified</span> : null}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

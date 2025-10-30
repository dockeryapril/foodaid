'use client';

import { useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { geocodeNominatim } from '../lib/geo';
import Link from 'next/link';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const sb = createClient(supabaseUrl, supabaseKey);

export default function SubmitPage(){
  const [form, setForm] = useState({
    title:'', description:'', organizer:'', event_date_start:'',
    address:'', city:'', state:'', postal_code:'',
    contact_url:'', submitted_by:''
  });
  const [geo, setGeo] = useState<{lat:number|undefined, lon:number|undefined, display?:string}>({lat: undefined, lon: undefined});
  const [status, setStatus] = useState<string>('');

  const onGeocode = async () => {
    setStatus('Geocoding…');
    const q = [form.address, form.city, form.state, form.postal_code].filter(Boolean).join(', ');
    const g = await geocodeNominatim(q);
    if(!g){ setStatus('No match found'); return; }
    setGeo({lat:g.lat, lon:g.lon, display:g.display});
    setStatus(`Matched: ${g.display}`);
  };

  const onSubmit = async (e:any) => {
    e.preventDefault();
    setStatus('Submitting…');
    const payload:any = {
      title: form.title || null,
      description: form.description || null,
      organizer: form.organizer || null,
      event_date_start: form.event_date_start ? new Date(form.event_date_start).toISOString() : null,
      address: form.address || null,
      city: form.city || null,
      state: form.state || null,
      postal_code: form.postal_code || null,
      latitude: geo.lat ?? null,
      longitude: geo.lon ?? null,
      contact_url: form.contact_url || null,
      submitted_by: form.submitted_by || null
    };
    const { error } = await sb.from('submissions').insert(payload);
    if(error){ setStatus('Error: ' + error.message); return; }
    setStatus('Thanks! Your submission is queued for review.');
    setForm({ title:'', description:'', organizer:'', event_date_start:'', address:'', city:'', state:'', postal_code:'', contact_url:'', submitted_by:'' });
    setGeo({lat: undefined, lon: undefined});
  };

  return (
    <div className="container">
      <h1>Submit a Food Assistance Event</h1>
      <p>Share verified food distributions, pantries, school meals, or mutual aid drops. A moderator will review before publishing.</p>
      <form onSubmit={onSubmit} className="list" style={{maxWidth:680}}>
        <input placeholder="Title (e.g., Mobile Pantry - SE Atlanta)" value={form.title} onChange={e=>setForm({...form, title:e.target.value})}/>
        <textarea placeholder="Description (date, time, ID requirements, what to bring)" value={form.description} onChange={e=>setForm({...form, description:e.target.value})}/>
        <input placeholder="Organizer (food bank, school, church, mutual aid)" value={form.organizer} onChange={e=>setForm({...form, organizer:e.target.value})}/>
        <input type="datetime-local" placeholder="Start date/time" value={form.event_date_start} onChange={e=>setForm({...form, event_date_start:e.target.value})}/>
        <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:8}}>
          <input placeholder="Address" value={form.address} onChange={e=>setForm({...form, address:e.target.value})}/>
          <input placeholder="City" value={form.city} onChange={e=>setForm({...form, city:e.target.value})}/>
          <input placeholder="State (GA, MI…)" value={form.state} onChange={e=>setForm({...form, state:e.target.value})}/>
          <input placeholder="Postal code" value={form.postal_code} onChange={e=>setForm({...form, postal_code:e.target.value})}/>
        </div>
        <div style={{display:'flex', gap:8}}>
          <button type="button" onClick={onGeocode}>Geocode</button>
          <span>{geo.display ? geo.display : ''}</span>
        </div>
        <input placeholder="Link for details (optional)" value={form.contact_url} onChange={e=>setForm({...form, contact_url:e.target.value})}/>
        <input placeholder="Your email or handle (optional, kept private)" value={form.submitted_by} onChange={e=>setForm({...form, submitted_by:e.target.value})}/>
        <button type="submit">Submit</button>
        <p style={{opacity:0.7}}>{status}</p>
      </form>
      <p style={{marginTop:16}}><Link href="/">Back to map</Link></p>
    </div>
  );
}

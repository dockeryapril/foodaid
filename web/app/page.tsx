'use client';

import { createClient } from '@supabase/supabase-js';
import { useEffect, useMemo, useState } from 'react';
import dynamic from 'next/dynamic';
import Filters from './components/Filters';
import ResultList from './components/ResultList';
import Link from 'next/link';

const Map = dynamic(() => import('./components/MapView'), { ssr: false });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const sb = createClient(supabaseUrl, supabaseKey);

type EventRow = {
  id: number;
  description: string | null;
  organizer: string | null;
  event_date_start: string | null;
  city: string | null;
  state: string | null;
  latitude: number | null;
  longitude: number | null;
  verified: boolean | null;
};

export default function Page() {
  const [rows, setRows] = useState<EventRow[]>([]);
  const [qState, setQState] = useState('');
  const [qCity, setQCity] = useState('');
  const [onlyVerified, setOnlyVerified] = useState(false);

  useEffect(() => {
    const run = async () => {
      const { data } = await sb
        .from('events')
        .select('id, description, organizer, event_date_start, city, state, latitude, longitude, verified')
        .gte('event_date_start', new Date(Date.now() - 1000*60*60*24*7).toISOString())
        .order('event_date_start', { ascending: true })
        .limit(500);
      if (data) setRows(data as EventRow[]);
    };
    run();
  }, []);

  const filtered = useMemo(() => {
    return rows.filter(r => {
      if (qState && (r.state || '').toLowerCase() !== qState.toLowerCase()) return false;
      if (qCity && (r.city || '').toLowerCase() !== qCity.toLowerCase()) return false;
      if (onlyVerified && !r.verified) return false;
      return true;
    });
  }, [rows, qState, qCity, onlyVerified]);

  return (
    <div className="container">
      <div className="header">
        <h1>Food Help Map</h1>
        <span className="badge">{filtered.length} results</span>
      </div>
      <div style={{display:'flex', gap:12, alignItems:'center'}}>
        <Filters onState={setQState} onCity={setQCity} onVerified={setOnlyVerified} />
        <Link href="/submit" className="badge" style={{textDecoration:'none'}}>Submit event</Link>
      </div>
      <Map rows={filtered} />
      <ResultList rows={filtered} />
    </div>
  );
}

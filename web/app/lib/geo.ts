export async function geocodeNominatim(query: string){
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`;
  const res = await fetch(url, { headers: { 'Accept-Language': 'en' } });
  if(!res.ok) return null;
  const data = await res.json();
  if(!Array.isArray(data) || data.length === 0) return null;
  const first = data[0];
  return { lat: parseFloat(first.lat), lon: parseFloat(first.lon), display: first.display_name };
}

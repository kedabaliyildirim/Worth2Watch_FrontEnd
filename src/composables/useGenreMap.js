// TMDB returns localised genre names (we built the catalog in tr-TR, so
// they come back Turkish). The UI is English, so we map back at display
// time without rebuilding the catalog. Anything not in this map falls
// through unchanged.

const TR_TO_EN = {
  'Aile': 'Family',
  'Aksiyon': 'Action',
  'Aksiyon & Macera': 'Action & Adventure',
  'Animasyon': 'Animation',
  'Belgesel': 'Documentary',
  'Bilim Kurgu & Fantazi': 'Sci-Fi & Fantasy',
  'Bilim-Kurgu': 'Science Fiction',
  'Çocuklar': 'Kids',
  'Dram': 'Drama',
  'Fantastik': 'Fantasy',
  'Gerçeklik': 'Reality',
  'Gerilim': 'Thriller',
  'Gizem': 'Mystery',
  'Haber': 'News',
  'Komedi': 'Comedy',
  'Konuşma': 'Talk',
  'Korku': 'Horror',
  'Macera': 'Adventure',
  'Müzik': 'Music',
  'Politik': 'Politics',
  'Romantik': 'Romance',
  'Savaş': 'War',
  'Savaş & Politik': 'War & Politics',
  'Suç': 'Crime',
  'Tarih': 'History',
  'TV Filmi': 'TV Movie',
  'TV film': 'TV Movie',
  'Vahşi Batı': 'Western',
  'Yabancı': 'Foreign',
}

export function translateGenre(g) {
  return TR_TO_EN[g] || g
}

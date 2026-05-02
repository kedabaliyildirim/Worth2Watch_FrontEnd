// Backend gerçek deploy'da yokken UI'ın çalışmaya devam etmesi için
// kullanılan örnek liste. Gerçek backend `:8000`'de ayağa kalktığında
// store fetch'leri ona düşer; bu sadece offline / demo modu.

const PROVIDER = (id, name, logo_path) => ({
  provider_id: id,
  provider_name: name,
  logo_path,
})

const NETFLIX = PROVIDER(8, 'Netflix', '/t2yyOv40HZeVlLjYsCsPHnWLk4W.jpg')
const PRIME = PROVIDER(
  9,
  'Amazon Prime Video',
  '/emthp39XA2YScoYL1p0sdbAH2WA.jpg'
)
const DISNEY = PROVIDER(337, 'Disney Plus', '/97yvRBw1GzX7fXprcF80er19ot.jpg')
const APPLE = PROVIDER(2, 'Apple TV', '/9ghgSC0MA082EL6HLCW3GalykFD.jpg')
const HBO = PROVIDER(384, 'HBO Max', '/Ajqyt5aNxNGjmF9uOfxArGrdf3X.jpg')

export const MOCK_MOVIES = [
  {
    movieName: 'Dune: Part Two',
    movieReleaseDate: '2024-03-01',
    movieGenre: 'Sci-Fi · Adventure',
    imdbRating: 8.5,
    tmdbRating: 8.3,
    rottenTomatoesRating: 92,
    movieRuntime: 166,
    overview:
      "Paul Atreides, kabilelerle birlikte ailesini katleden komplocuların intikamını almak için Chani ve Fremen'lerle ittifak kurar. Geleceğe dair vizyonlar arasında galaksi çapında bir savaş ile sevdiklerini yitirmek arasında seçim yapmak zorunda kalır.",
    movieProviders: [HBO, APPLE],
    imageURL:
      'https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/87zPiUBEi0OctyT1g8DfwfBgC1L.jpg',
    youtubeId: 'Way9Dexny3w',
  },
  {
    movieName: 'Oppenheimer',
    movieReleaseDate: '2023-07-21',
    movieGenre: 'Drama · Biography · History',
    imdbRating: 8.4,
    tmdbRating: 8.1,
    rottenTomatoesRating: 93,
    movieRuntime: 180,
    overview:
      "Atom bombasını yaratan adamın hikâyesi: J. Robert Oppenheimer'ın Manhattan Projesi'ndeki yükselişi ve çöküşü. Christopher Nolan'ın IMAX 70mm formatında çektiği üç saatlik bir kontrast çalışması.",
    movieProviders: [PRIME, APPLE],
    imageURL:
      'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/rLb2cwF3Pazuxaj0sRXQ037tGI1.jpg',
    youtubeId: 'uYPbbksJxIg',
  },
  {
    movieName: 'Poor Things',
    movieReleaseDate: '2023-12-08',
    movieGenre: 'Sci-Fi · Comedy · Romance',
    imdbRating: 8.0,
    tmdbRating: 7.8,
    rottenTomatoesRating: 92,
    movieRuntime: 141,
    overview:
      "Yorgos Lanthimos'un Frankenstein-vari masalı: bir bilim adamı tarafından yeniden hayata döndürülen genç bir kadının dünyayı keşfedişi. Görsel olarak çılgın, hikâye olarak provokatif.",
    movieProviders: [DISNEY],
    imageURL:
      'https://image.tmdb.org/t/p/w500/kCGlIMHnOm8JPXq3rXM6c5wMxcT.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/q47umIdwxLdmQUk8exqaRtBnao9.jpg',
    youtubeId: 'RlbR5N6veqw',
  },
  {
    movieName: 'The Holdovers',
    movieReleaseDate: '2023-11-10',
    movieGenre: 'Drama · Comedy',
    imdbRating: 7.9,
    tmdbRating: 7.7,
    rottenTomatoesRating: 96,
    movieRuntime: 133,
    overview:
      'Yatılı bir okulda Noel tatilinde mahsur kalan üç farklı insan: huysuz bir öğretmen, yaramaz bir öğrenci ve yas tutan bir aşçı. Alexander Payne nostaljik 70’ler dokusuyla çekti.',
    movieProviders: [PRIME],
    imageURL:
      'https://image.tmdb.org/t/p/w500/VkRdcNKNPMxDTeoKVCx39K3X9C.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/uyyuGGitJUGSyrS7ldERUbGyhb6.jpg',
    youtubeId: 'cRJ-CuFu0Tc',
  },
  {
    movieName: 'Anatomy of a Fall',
    movieReleaseDate: '2023-08-23',
    movieGenre: 'Crime · Drama · Thriller',
    imdbRating: 7.7,
    tmdbRating: 7.6,
    rottenTomatoesRating: 96,
    movieRuntime: 152,
    overview:
      "Sandra'nın kocası evlerinin önündeki karda ölü bulunur — kaza mı, intihar mı, cinayet mi? Mahkemede evliliğin tüm karanlık köşeleri açılır. Justine Triet'in Altın Palmiye'si.",
    movieProviders: [APPLE, HBO],
    imageURL:
      'https://image.tmdb.org/t/p/w500/kQs6keheMwCxJxrzV83VUwFtHkB.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/vlT4P0VRViKtO5oLg8OtR6ENpiJ.jpg',
    youtubeId: 'ApGxtU3-XU8',
  },
  {
    movieName: 'Past Lives',
    movieReleaseDate: '2023-06-02',
    movieGenre: 'Romance · Drama',
    imdbRating: 7.9,
    tmdbRating: 7.8,
    rottenTomatoesRating: 96,
    movieRuntime: 105,
    overview:
      'Çocukluk aşkları Nora ve Hae Sung 24 yıl sonra New York’ta bir hafta için yeniden buluşur. Kaderin, geçmişin ve “in-yun” kavramının kırılgan bir meditasyonu.',
    movieProviders: [PRIME],
    imageURL:
      'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/yRRuLwOhk2DGKj9Pi6Pj5lAxbsi.jpg',
    youtubeId: 'wU-no7yjEFE',
  },
  {
    movieName: 'Killers of the Flower Moon',
    movieReleaseDate: '2023-10-20',
    movieGenre: 'Crime · Drama · History',
    imdbRating: 7.6,
    tmdbRating: 7.5,
    rottenTomatoesRating: 93,
    movieRuntime: 206,
    overview:
      "Scorsese'nin Osage Nation cinayetleri üzerine 3.5 saatlik destanı. DiCaprio + De Niro + Lily Gladstone, Amerikan tarihinin en utanç verici sayfalarından birini açıyor.",
    movieProviders: [APPLE],
    imageURL:
      'https://image.tmdb.org/t/p/w500/dB6Krk806zeqd0YNp2ngQ9zXteH.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/1X7vow16X7CnCoexXh4H4F2yDJv.jpg',
    youtubeId: 'EP34Yoxs3FQ',
  },
  {
    movieName: 'Spider-Man: Across the Spider-Verse',
    movieReleaseDate: '2023-06-02',
    movieGenre: 'Animation · Action · Adventure',
    imdbRating: 8.6,
    tmdbRating: 8.4,
    rottenTomatoesRating: 95,
    movieRuntime: 140,
    overview:
      "Miles Morales, çoklu evrene dağılmış Spider-Man'lerle tanışır ve Spider-Society'nin neye değer biçtiği konusunda onlarla çatışır. Bir film değil, taşınabilir bir sanat galerisi.",
    movieProviders: [NETFLIX, PRIME],
    imageURL:
      'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/4HodYYKEIsGOdinkGi2Ucfxbgqq.jpg',
    youtubeId: 'cqGjhVJWtEg',
  },
  {
    movieName: 'The Zone of Interest',
    movieReleaseDate: '2023-12-15',
    movieGenre: 'Drama · History · War',
    imdbRating: 7.4,
    tmdbRating: 7.0,
    rottenTomatoesRating: 92,
    movieRuntime: 105,
    overview:
      "Auschwitz komutanı ve ailesinin kamp duvarının hemen yanındaki sıradan ev hayatı. Jonathan Glazer kötülüğün banalliğini ses tasarımıyla yakalıyor — kareye girmeyen şey en korkunç olanı.",
    movieProviders: [HBO],
    imageURL:
      'https://image.tmdb.org/t/p/w500/hUu9zyZmDd8VZegKi1iK1Vk0RYS.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/2v3HZD6IT9bpYaPPSWa1A1f4OQs.jpg',
    youtubeId: 'kV5ufNcPRyA',
  },
  {
    movieName: 'Barbie',
    movieReleaseDate: '2023-07-21',
    movieGenre: 'Comedy · Adventure · Fantasy',
    imdbRating: 6.8,
    tmdbRating: 7.1,
    rottenTomatoesRating: 88,
    movieRuntime: 114,
    overview:
      "Greta Gerwig'in pembe matrix'i: Barbie, Barbieland'in mükemmelliğinden gerçek dünyaya düşer ve patriyarka ile yüzleşir. Hem ticari blockbuster hem de meta-yorum.",
    movieProviders: [HBO, PRIME],
    imageURL:
      'https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/ctMserH8g2SeOAnCw5gFjdQF8mo.jpg',
    youtubeId: 'pBk4NYhWNMM',
  },
  {
    movieName: 'Inception',
    movieReleaseDate: '2010-07-16',
    movieGenre: 'Sci-Fi · Action · Thriller',
    imdbRating: 8.8,
    tmdbRating: 8.4,
    rottenTomatoesRating: 87,
    movieRuntime: 148,
    overview:
      "Bilinçaltına girip fikir çalan adam, bu kez ters bir göreve çıkar: bir fikri yerleştirmek. Nolan'ın altı katmanlı rüya çantası.",
    movieProviders: [NETFLIX, PRIME],
    imageURL:
      'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/s3TBrRGB1iav7gFOCNx3H31MoES.jpg',
    youtubeId: 'YoHD9XEInc0',
  },
  {
    movieName: 'Parasite',
    movieReleaseDate: '2019-05-30',
    movieGenre: 'Drama · Thriller · Comedy',
    imdbRating: 8.5,
    tmdbRating: 8.5,
    rottenTomatoesRating: 99,
    movieRuntime: 132,
    overview:
      "Yoksul Kim ailesi zengin Park ailesinin evine yavaş yavaş sızar. Bong Joon-ho'nun sınıf çatışmasına bakan Altın Palmiye + 4 Oscar'lı zekası.",
    movieProviders: [PRIME, APPLE],
    imageURL:
      'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
    backdropURL:
      'https://image.tmdb.org/t/p/original/TU9NIjwzjoKPwQHoHshkBcQZzr.jpg',
    youtubeId: '5xH0HfJHsaY',
  },
]

// Page-aware getter so the existing pagination wiring keeps working
// against mock data. Keeps shape consistent with whatever the original
// `/allmovies` endpoint returned.
export function pagedMockMovies({ page = 1, pageSize = 20 } = {}) {
  const start = (page - 1) * pageSize
  return MOCK_MOVIES.slice(start, start + pageSize)
}

export function topTenMockMovies() {
  return [...MOCK_MOVIES]
    .sort((a, b) => (b.imdbRating || 0) - (a.imdbRating || 0))
    .slice(0, 10)
}

export const MOCK_TOTAL_PAGES = Math.ceil(MOCK_MOVIES.length / 20)

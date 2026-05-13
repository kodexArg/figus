import type { MockUser } from './types';
import { STICKERS } from './stickers';

interface UserSeed {
  id: string;
  name: string;
  city: string;
  lat: number;
  lng: number;
  contacts: MockUser['contacts'];
  rating: number;
  trades: number;
}

const SEEDS: UserSeed[] = [
  { id: 'u01', name: 'Martín Sosa', city: 'CABA', lat: -34.6037, lng: -58.3816, contacts: { whatsapp: '+5491133334444', instagram: '@martinsosa' }, rating: 4.8, trades: 32 },
  { id: 'u02', name: 'Lucía Fernández', city: 'La Plata', lat: -34.9215, lng: -57.9545, contacts: { whatsapp: '+5492216667777', telegram: '@lufer' }, rating: 4.6, trades: 18 },
  { id: 'u03', name: 'Joaquín Vera', city: 'Rosario', lat: -32.9442, lng: -60.6505, contacts: { instagram: '@jvera_figus', email: 'joaco@mail.com' }, rating: 4.9, trades: 47 },
  { id: 'u04', name: 'Camila Ríos', city: 'Córdoba', lat: -31.4201, lng: -64.1888, contacts: { whatsapp: '+5493515551122' }, rating: 4.3, trades: 12 },
  { id: 'u05', name: 'Federico Paz', city: 'Mendoza', lat: -32.8895, lng: -68.8458, contacts: { whatsapp: '+5492614443322', instagram: '@fedepaz' }, rating: 4.5, trades: 21 },
  { id: 'u06', name: 'Sofía Quiroga', city: 'Mar del Plata', lat: -38.0055, lng: -57.5426, contacts: { telegram: '@sofiq', email: 'sofi.q@mail.com' }, rating: 4.7, trades: 26 },
  { id: 'u07', name: 'Diego Acuña', city: 'San Miguel de Tucumán', lat: -26.8083, lng: -65.2176, contacts: { whatsapp: '+5493814445566' }, rating: 4.2, trades: 9 },
  { id: 'u08', name: 'Valentina Cruz', city: 'Salta', lat: -24.7821, lng: -65.4232, contacts: { instagram: '@valecruz', whatsapp: '+5493874448899' }, rating: 4.9, trades: 38 },
  { id: 'u09', name: 'Bruno Iglesias', city: 'Neuquén', lat: -38.9516, lng: -68.0591, contacts: { whatsapp: '+5492995552211' }, rating: 4.4, trades: 14 },
  { id: 'u10', name: 'Agustina Molina', city: 'Bariloche', lat: -41.1335, lng: -71.3103, contacts: { instagram: '@aguspatagonia', telegram: '@agusm' }, rating: 4.8, trades: 29 },
  { id: 'u11', name: 'Tomás Herrera', city: 'CABA', lat: -34.5895, lng: -58.4173, contacts: { whatsapp: '+5491155556677' }, rating: 4.1, trades: 7 },
  { id: 'u12', name: 'Florencia Díaz', city: 'San Isidro', lat: -34.4708, lng: -58.5128, contacts: { instagram: '@flordiaz', email: 'flor@mail.com' }, rating: 4.6, trades: 19 },
  { id: 'u13', name: 'Nicolás Soto', city: 'Bahía Blanca', lat: -38.7196, lng: -62.2724, contacts: { whatsapp: '+5492914443311' }, rating: 4.3, trades: 11 },
  { id: 'u14', name: 'Julieta Bravo', city: 'Resistencia', lat: -27.4519, lng: -58.9866, contacts: { telegram: '@julibravo' }, rating: 4.5, trades: 16 },
  { id: 'u15', name: 'Ezequiel Núñez', city: 'Posadas', lat: -27.3621, lng: -55.9008, contacts: { whatsapp: '+5493764449988', instagram: '@ezenunez' }, rating: 4.7, trades: 22 },
  { id: 'u16', name: 'Carla Medina', city: 'Santa Fe', lat: -31.6107, lng: -60.6973, contacts: { whatsapp: '+5493425551177' }, rating: 4.4, trades: 13 },
  { id: 'u17', name: 'Ignacio Pereyra', city: 'San Juan', lat: -31.5375, lng: -68.5364, contacts: { instagram: '@nachoper' }, rating: 4.0, trades: 6 },
  { id: 'u18', name: 'Romina Gallardo', city: 'Río Cuarto', lat: -33.1232, lng: -64.3493, contacts: { whatsapp: '+5493584446655', telegram: '@romi_g' }, rating: 4.6, trades: 17 },
  { id: 'u19', name: 'Maximiliano Ortega', city: 'CABA', lat: -34.6158, lng: -58.4333, contacts: { whatsapp: '+5491166667788', email: 'maxi@mail.com' }, rating: 4.9, trades: 41 },
  { id: 'u20', name: 'Antonella Vázquez', city: 'Quilmes', lat: -34.7203, lng: -58.2542, contacts: { instagram: '@antovaz' }, rating: 4.5, trades: 15 },
  { id: 'u21', name: 'Gonzalo Reyes', city: 'Montevideo (UY)', lat: -34.9011, lng: -56.1645, contacts: { whatsapp: '+59899441122', telegram: '@gonzar' }, rating: 4.8, trades: 33 },
  { id: 'u22', name: 'Mariana Espinoza', city: 'Asunción (PY)', lat: -25.2637, lng: -57.5759, contacts: { whatsapp: '+595981554433' }, rating: 4.4, trades: 12 },
  { id: 'u23', name: 'Pablo Méndez', city: 'Santiago (CL)', lat: -33.4489, lng: -70.6693, contacts: { instagram: '@pablomdz', whatsapp: '+56987661122' }, rating: 4.7, trades: 24 },
  { id: 'u24', name: 'Renata Aguilar', city: 'CABA', lat: -34.6083, lng: -58.3712, contacts: { telegram: '@renaag', email: 'rena@mail.com' }, rating: 4.6, trades: 20 },
  { id: 'u25', name: 'Cristian Funes', city: 'Mendoza', lat: -32.9078, lng: -68.8500, contacts: { whatsapp: '+5492614448811' }, rating: 4.2, trades: 8 },
  { id: 'u26', name: 'Bárbara Coronel', city: 'San Salvador de Jujuy', lat: -24.1858, lng: -65.2995, contacts: { instagram: '@barbcoronel' }, rating: 4.5, trades: 16 },
  { id: 'u27', name: 'Leandro Vidal', city: 'La Pampa - Santa Rosa', lat: -36.6167, lng: -64.2833, contacts: { whatsapp: '+5492954443377' }, rating: 4.3, trades: 11 },
  { id: 'u28', name: 'Paula Benítez', city: 'Corrientes', lat: -27.4691, lng: -58.8309, contacts: { whatsapp: '+5493794445522', telegram: '@paulab' }, rating: 4.7, trades: 25 },
  { id: 'u29', name: 'Mauricio Cabrera', city: 'Comodoro Rivadavia', lat: -45.8645, lng: -67.4969, contacts: { instagram: '@mauchubut' }, rating: 4.4, trades: 13 },
  { id: 'u30', name: 'Elena Ponce', city: 'Ushuaia', lat: -54.8019, lng: -68.3030, contacts: { whatsapp: '+5492901111222', email: 'elenap@mail.com' }, rating: 4.9, trades: 36 },
];

function makeRng(seed: number) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6D2B79F5) | 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function buildInventory(seed: number) {
  const rng = makeRng(seed);
  const inventory: Record<string, number> = {};
  const wants: string[] = [];
  for (const s of STICKERS) {
    const r = rng();
    // Mystery players and coca-cola: ownership rate way lower
    const ownChance = (s.type === 'mystery_player' || s.type === 'coca_cola_special') ? 0.15 : 0.55;
    if (r < ownChance) {
      const dupRoll = rng();
      const count = dupRoll < 0.22 ? 1 + Math.floor(rng() * 4) + 1 : 1;
      inventory[s.id] = count;
    } else {
      wants.push(s.id);
    }
  }
  return { inventory, wants };
}

export const USERS: MockUser[] = SEEDS.map((seed, i) => {
  const { inventory, wants } = buildInventory(i * 1000 + 13);
  return { ...seed, inventory, wants };
});

export const USERS_BY_ID: Record<string, MockUser> = Object.fromEntries(
  USERS.map((u) => [u.id, u]),
);

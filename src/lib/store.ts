import type { CollectionState, Profile } from '../data/types';

const COLLECTION_KEY = 'figus.collection.v1';
const PROFILE_KEY = 'figus.profile.v1';

type Listener = () => void;
const listeners = new Set<Listener>();

export function subscribe(fn: Listener): () => void {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

function emit() {
  listeners.forEach((fn) => fn());
}

export function getCollection(): CollectionState {
  if (typeof localStorage === 'undefined') return {};
  try {
    const raw = localStorage.getItem(COLLECTION_KEY);
    return raw ? (JSON.parse(raw) as CollectionState) : {};
  } catch {
    return {};
  }
}

export function setCollection(state: CollectionState) {
  localStorage.setItem(COLLECTION_KEY, JSON.stringify(state));
  emit();
}

export function getCount(id: string): number {
  return getCollection()[id] ?? 0;
}

export function setCount(id: string, count: number) {
  const c = getCollection();
  if (count <= 0) {
    delete c[id];
  } else {
    c[id] = count;
  }
  setCollection(c);
}

export function increment(id: string) {
  setCount(id, getCount(id) + 1);
}

export function decrement(id: string) {
  setCount(id, getCount(id) - 1);
}

export function toggleOwned(id: string) {
  setCount(id, getCount(id) > 0 ? 0 : 1);
}

const DEFAULT_PROFILE: Profile = {
  name: '',
  city: '',
  lat: null,
  lng: null,
  contacts: {},
};

export function getProfile(): Profile {
  if (typeof localStorage === 'undefined') return DEFAULT_PROFILE;
  try {
    const raw = localStorage.getItem(PROFILE_KEY);
    return raw ? { ...DEFAULT_PROFILE, ...JSON.parse(raw) } : DEFAULT_PROFILE;
  } catch {
    return DEFAULT_PROFILE;
  }
}

export function setProfile(profile: Profile) {
  localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
  emit();
}

export function clearAll() {
  localStorage.removeItem(COLLECTION_KEY);
  localStorage.removeItem(PROFILE_KEY);
  emit();
}

export function seedDemoCollection(seed = 42) {
  // Quick seed: ~40% owned, of which ~25% duplicated, so user has something to play with.
  import('../data/stickers').then(({ STICKERS }) => {
    let s = seed >>> 0;
    const rng = () => {
      s = (s + 0x6D2B79F5) | 0;
      let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
    const c: CollectionState = {};
    for (const sticker of STICKERS) {
      const r = rng();
      if (r < 0.4) {
        const dup = rng();
        c[sticker.id] = dup < 0.25 ? 1 + Math.floor(rng() * 3) + 1 : 1;
      }
    }
    setCollection(c);
  });
}

import type { CollectionState, MockUser, Profile, Sticker } from '../data/types';
import { USERS } from '../data/users';
import { STICKERS_BY_ID } from '../data/stickers';
import { haversineKm } from './geo';

export interface SuggestionMatch {
  user: MockUser;
  count: number;
  distanceKm?: number;
  reciprocity: number; // how many of their wants I have as duplicates
}

export interface Suggestion {
  sticker: Sticker;
  matches: SuggestionMatch[];
  score: number;
}

export function buildSuggestions(
  collection: CollectionState,
  profile: Profile | null,
  opts: { limit?: number; maxDistanceKm?: number } = {},
): Suggestion[] {
  const { limit = 30, maxDistanceKm = 1500 } = opts;

  const myDuplicates = new Set(
    Object.entries(collection)
      .filter(([, n]) => n > 1)
      .map(([id]) => id),
  );

  const missingIds = Object.values(STICKERS_BY_ID)
    .filter((s) => (collection[s.id] ?? 0) === 0)
    .map((s) => s.id);

  const here = profile && profile.lat != null && profile.lng != null
    ? { lat: profile.lat, lng: profile.lng }
    : null;

  const suggestions: Suggestion[] = [];

  for (const id of missingIds) {
    const sticker = STICKERS_BY_ID[id];
    const matches: SuggestionMatch[] = [];

    for (const user of USERS) {
      const count = user.inventory[id] ?? 0;
      if (count <= 1) continue; // they need at least 1 duplicate
      const distanceKm = here ? haversineKm(here, user) : undefined;
      if (distanceKm !== undefined && distanceKm > maxDistanceKm) continue;
      const reciprocity = user.wants.filter((w) => myDuplicates.has(w)).length;
      matches.push({ user, count, distanceKm, reciprocity });
    }

    if (matches.length === 0) continue;

    // Score: more matches > closer > higher reciprocity > rarer sticker
    const closest = matches.reduce(
      (acc, m) => Math.min(acc, m.distanceKm ?? Number.POSITIVE_INFINITY),
      Number.POSITIVE_INFINITY,
    );
    const proximity = Number.isFinite(closest) ? 1 / (1 + closest / 50) : 0.5;
    const reciprocityBonus = matches.reduce((a, m) => a + m.reciprocity, 0);
    const rarityBonus = sticker.rarity === 'legendary' ? 3 : sticker.rarity === 'rare' ? 1.5 : 1;
    const score = matches.length * 2 + proximity * 5 + reciprocityBonus * 0.3 + rarityBonus;

    matches.sort((a, b) => {
      const da = a.distanceKm ?? Number.POSITIVE_INFINITY;
      const db = b.distanceKm ?? Number.POSITIVE_INFINITY;
      if (da !== db) return da - db;
      return b.reciprocity - a.reciprocity;
    });

    suggestions.push({ sticker, matches: matches.slice(0, 5), score });
  }

  suggestions.sort((a, b) => b.score - a.score);
  return suggestions.slice(0, limit);
}

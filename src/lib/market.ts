import type { MarketListing, Profile } from '../data/types';
import { USERS } from '../data/users';
import { STICKERS_BY_ID } from '../data/stickers';
import { haversineKm } from './geo';

export interface MarketFilters {
  query?: string;
  team?: string;
  type?: string;
  maxDistanceKm?: number;
  onlyLegendary?: boolean;
}

export function buildMarket(
  profile: Profile | null,
  filters: MarketFilters = {},
): MarketListing[] {
  const here = profile && profile.lat != null && profile.lng != null
    ? { lat: profile.lat, lng: profile.lng }
    : null;

  const listings: MarketListing[] = [];
  for (const user of USERS) {
    for (const [stickerId, count] of Object.entries(user.inventory)) {
      if (count <= 1) continue; // only duplicates are tradeable
      const sticker = STICKERS_BY_ID[stickerId];
      if (!sticker) continue;
      const distanceKm = here ? haversineKm(here, user) : undefined;
      listings.push({ user, sticker, count: count - 1, distanceKm });
    }
  }

  return listings
    .filter((l) => {
      if (filters.type && !filters.type.split(',').includes(l.sticker.type)) return false;
      if (filters.team && l.sticker.team?.code !== filters.team) return false;
      if (filters.onlyLegendary && l.sticker.rarity !== 'legendary') return false;
      if (filters.maxDistanceKm !== undefined && l.distanceKm !== undefined && l.distanceKm > filters.maxDistanceKm) return false;
      if (filters.query) {
        const q = filters.query.toLowerCase();
        const teamName = l.sticker.team?.name_es.toLowerCase() ?? '';
        if (!l.sticker.label.toLowerCase().includes(q) && !l.sticker.code.toLowerCase().includes(q) && !teamName.includes(q)) {
          return false;
        }
      }
      return true;
    })
    .sort((a, b) => {
      const da = a.distanceKm ?? Number.POSITIVE_INFINITY;
      const db = b.distanceKm ?? Number.POSITIVE_INFINITY;
      if (da !== db) return da - db;
      return b.user.rating - a.user.rating;
    });
}

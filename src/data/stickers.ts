import catalog from './catalog.json';
import { TEAM_BY_ID } from './teams';
import type { RawSticker, Sticker, Rarity, StickerType } from './types';

function rarityOf(s: RawSticker): Rarity {
  if (s.type === 'legend') return 'legendary';
  if (s.type === 'coca_cola_special') return 'legendary';
  if (s.type === 'mystery_player') return s.parallel_variant === 'regular' ? 'rare' : 'parallel';
  if (s.is_foil) return 'foil';
  if (s.type === 'team_emblem' || s.type === 'team_photo' || s.type === 'host_country' || s.type === 'official_emblem' || s.type === 'official_ball' || s.type === 'mascot' || s.type === 'panini_logo' || s.type === 'slogan') return 'rare';
  return 'common';
}

const TYPE_ORDER: StickerType[] = [
  'panini_logo', 'official_emblem', 'mascot', 'slogan', 'official_ball',
  'host_country', 'team_emblem', 'team_photo', 'player',
  'legend', 'mystery_player', 'coca_cola_special',
];
const TYPE_INDEX: Record<string, number> = Object.fromEntries(TYPE_ORDER.map((t, i) => [t, i]));

function compareForNumbering(a: RawSticker, b: RawSticker): number {
  // Stickers with album_position keep that order
  if (a.album_position != null && b.album_position != null) {
    return a.album_position - b.album_position;
  }
  if (a.album_position != null) return -1;
  if (b.album_position != null) return 1;
  // Fallback: by type group, then by code
  const ta = TYPE_INDEX[a.type] ?? 999;
  const tb = TYPE_INDEX[b.type] ?? 999;
  if (ta !== tb) return ta - tb;
  return a.code.localeCompare(b.code);
}

export const STICKERS: Sticker[] = (catalog.stickers as RawSticker[])
  .slice()
  .sort(compareForNumbering)
  .map((s, i) => ({
    ...s,
    team: s.team_id ? TEAM_BY_ID[s.team_id] : undefined,
    rarity: rarityOf(s),
    number: i + 1,
  }));

export const STICKERS_BY_ID: Record<string, Sticker> = Object.fromEntries(
  STICKERS.map((s) => [s.id, s]),
);

export const TOTAL_STICKERS = STICKERS.length;

export const ALBUM_STICKERS = STICKERS.filter((s) => s.album_position != null);
export const EXTRA_STICKERS = STICKERS.filter((s) => s.type === 'mystery_player');
export const COCA_STICKERS = STICKERS.filter((s) => s.type === 'coca_cola_special');

export const TYPE_LABELS: Record<StickerType, string> = {
  panini_logo: 'Panini',
  official_emblem: 'Emblema oficial',
  mascot: 'Mascota',
  slogan: 'Slogan',
  official_ball: 'Balón',
  host_country: 'Anfitrión',
  team_emblem: 'Escudo',
  team_photo: 'Plantel',
  player: 'Jugador',
  legend: 'Leyenda',
  coca_cola_special: 'Coca-Cola',
  mystery_player: 'Mystery',
};

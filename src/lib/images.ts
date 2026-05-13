import type { Sticker } from '../data/types';
import { flagUrl } from '../data/teams';

/**
 * Deterministic image source per sticker.
 * - team_emblem / host_country: flag from flagcdn (free CDN, no key)
 * - team_photo: DiceBear shapes seeded by team code (group photo placeholder)
 * - player / mystery_player / coca_cola_special / legend: DiceBear avatar seeded by label
 * - mascot / panini_logo / official_emblem / official_ball / slogan: returns null → emoji fallback in card
 */
export function stickerImageUrl(s: Sticker): string | null {
  if (s.type === 'team_emblem' && s.team) {
    return flagUrl(s.team.code, 160);
  }
  if (s.type === 'host_country') {
    const hostByCode: Record<string, string> = { 'FWC-5': 'USA', 'FWC-6': 'CAN', 'FWC-7': 'MEX' };
    const code = hostByCode[s.code];
    if (code) return flagUrl(code, 160);
  }
  if (s.type === 'team_photo' && s.team) {
    return `https://api.dicebear.com/9.x/shapes/svg?seed=${encodeURIComponent(s.team.code + '-team')}&backgroundColor=1e293b`;
  }
  if (s.type === 'player' || s.type === 'mystery_player') {
    const seed = encodeURIComponent(s.label);
    return `https://api.dicebear.com/9.x/avataaars/svg?seed=${seed}&backgroundColor=0f172a`;
  }
  if (s.type === 'coca_cola_special') {
    const seed = encodeURIComponent(s.label);
    return `https://api.dicebear.com/9.x/avataaars/svg?seed=${seed}&backgroundColor=991b1b`;
  }
  if (s.type === 'legend') {
    const seed = encodeURIComponent(s.label);
    return `https://api.dicebear.com/9.x/lorelei/svg?seed=${seed}&backgroundColor=fbbf24`;
  }
  return null;
}

export function emojiForType(type: Sticker['type']): string {
  switch (type) {
    case 'mascot': return '🦅';
    case 'official_ball': return '⚽';
    case 'official_emblem': return '🏆';
    case 'panini_logo': return '📘';
    case 'slogan': return '✨';
    default: return '·';
  }
}

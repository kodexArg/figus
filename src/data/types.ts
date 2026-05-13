export type Confederation = 'CONMEBOL' | 'UEFA' | 'CONCACAF' | 'AFC' | 'CAF' | 'OFC';

export type StickerType =
  | 'panini_logo'
  | 'official_emblem'
  | 'mascot'
  | 'slogan'
  | 'official_ball'
  | 'host_country'
  | 'team_emblem'
  | 'team_photo'
  | 'player'
  | 'legend'
  | 'coca_cola_special'
  | 'mystery_player';

export type Rarity = 'common' | 'rare' | 'legendary' | 'foil' | 'parallel';

export interface Team {
  id: string;
  code: string;
  name_en: string;
  name_es: string;
  confederation: Confederation;
  is_host: boolean;
}

export interface RawSticker {
  id: string;
  code: string;
  album_position: number | null;
  label: string;
  type: StickerType;
  team_id: string | null;
  position_in_team: number | null;
  is_foil: boolean;
  parallel_set: string | null;
  parallel_variant: string | null;
}

export interface Sticker extends RawSticker {
  team?: Team;
  rarity: Rarity;
  number: number;
}

export interface UserContacts {
  whatsapp?: string;
  instagram?: string;
  telegram?: string;
  email?: string;
}

export interface MockUser {
  id: string;
  name: string;
  city: string;
  lat: number;
  lng: number;
  contacts: UserContacts;
  inventory: Record<string, number>;
  wants: string[];
  rating: number;
  trades: number;
}

export interface Profile {
  name: string;
  city: string;
  lat: number | null;
  lng: number | null;
  contacts: UserContacts;
}

export type CollectionState = Record<string, number>;

export interface MarketListing {
  user: MockUser;
  sticker: Sticker;
  count: number;
  distanceKm?: number;
}

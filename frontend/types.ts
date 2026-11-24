export interface OfferLink {
  id: number;
  offer_id: number;
  offer_name: string | null;
  share: number;
  is_pinned: boolean;
  status: "active" | "removed";
}

export interface Stream {
  id: number;
  name: string;
  position: number;
  has_offers: boolean;
  is_dirty: boolean;
  offers: OfferLink[];
}

export interface Campaign {
  id: number;
  name: string;
  alias: string | null;
}

export interface CatalogOffer {
  id: number;
  name: string;
}
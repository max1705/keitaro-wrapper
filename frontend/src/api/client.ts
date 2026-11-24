const BASE = "http://127.0.0.1:8000";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  return r.json();
}

export const api = {
  syncCampaigns: () => req("/campaigns/sync", { method: "POST" }),
  listCampaigns: () => req<import("../types").Campaign[]>("/campaigns"),
  fetchStreams: (cid: number) =>
    req(`/campaigns/${cid}/fetch`, { method: "POST" }),
  getStreams: (cid: number) =>
    req<import("../types").Stream[]>(`/campaigns/${cid}/streams`),
  getStream: (sid: number) =>
    req<import("../types").Stream>(`/streams/${sid}`),
  offersCatalog: () =>
    req<import("../types").CatalogOffer[]>("/streams/offers/catalog"),
  addOffer: (sid: number, offerId: number) =>
    req(`/streams/${sid}/offers`, {
      method: "POST",
      body: JSON.stringify({ offer_id: offerId }),
    }),
  removeOffer: (sid: number, offerId: number) =>
    req(`/streams/${sid}/offers/${offerId}`, { method: "DELETE" }),
  bringBack: (sid: number, offerId: number) =>
    req(`/streams/${sid}/offers/${offerId}/bring-back`, { method: "POST" }),
  togglePin: (sid: number, offerId: number) =>
    req(`/streams/${sid}/offers/${offerId}/pin`, { method: "POST" }),
  push: (sid: number) => req(`/streams/${sid}/push`, { method: "POST" }),
  cancel: (sid: number) => req(`/streams/${sid}/cancel`, { method: "POST" }),
};
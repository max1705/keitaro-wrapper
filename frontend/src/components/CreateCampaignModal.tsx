import { useState, useEffect, useMemo } from "react";
import type { CatalogOffer } from "../types";
import { api } from "../api/client";

interface Props {
  onClose: () => void;
  onCreated: () => void;
}

export function CreateCampaignModal({ onClose, onCreated }: Props) {
  const [name, setName] = useState("");
  const [geo, setGeo] = useState("");
  const [search, setSearch] = useState("");
  const [offerId, setOfferId] = useState<number | null>(null);
  const [catalog, setCatalog] = useState<CatalogOffer[]>([]);
  const [loading, setLoading] = useState(false);

  // Загружаем каталог офферов один раз при открытии
  useEffect(() => {
    api.offersCatalog().then(setCatalog);
  }, []);

  // Фильтруем офферы для автокомплита по ID или имени
  const filteredOffers = useMemo(() => {
    if (!search) return [];
    const lower = search.toLowerCase();
    return catalog
      .filter(o => o.id.toString().includes(search) || o.name.toLowerCase().includes(lower))
      .slice(0, 5); // Показываем максимум 5 результатов
  }, [catalog, search]);

  const handleCreate = async () => {
    if (!name || !geo || !offerId) return;
    setLoading(true);
    try {
      // Вызываем наш API
      await fetch("http://127.0.0.1:8000/campaigns/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, geo, offer_id: offerId }),
      });
      onCreated();
      onClose();
    } catch (e) {
      console.error(e);
      alert("Ошибка при создании кампании");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>New campaign</h2>
        
        <div className="form-group">
          <label>Name</label>
          <input 
            value={name} 
            onChange={e => setName(e.target.value)} 
            placeholder="Имя кампании" 
          />
        </div>

        <div className="form-group">
          <label>Geo</label>
          <input 
            value={geo} 
            onChange={e => setGeo(e.target.value)} 
            placeholder="MX, AU, RO..." 
          />
        </div>

        <div className="form-group offer-group">
          <label>Offer</label>
          <input
            value={search}
            onChange={e => { setSearch(e.target.value); setOfferId(null); }}
            placeholder="Поиск по ID или названию..."
          />
          {/* Выпадающий список автокомплита */}
          {filteredOffers.length > 0 && !offerId && (
            <ul className="autocomplete-list">
              {filteredOffers.map(o => (
                <li key={o.id} onClick={() => { setSearch(`${o.id} - ${o.name}`); setOfferId(o.id); }}>
                  {o.id} — {o.name}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="modal-actions">
          <button className="btn-cancel" onClick={onClose} disabled={loading}>Cancel</button>
          <button className="btn-create" onClick={handleCreate} disabled={!name || !geo || !offerId || loading}>
            {loading ? "Creating..." : "Create"}
          </button>
        </div>
      </div>
    </div>
  );
}
import { useEffect, useMemo, useState } from "react";
import type { CatalogOffer } from "../types";
import { api } from "../api/client";

interface Props {
  streamId: number;
  existing: number[];
  onDone: () => void;
  onCancel: () => void;
}

export function AddOfferRow({ streamId, existing, onDone, onCancel }: Props) {
  const [catalog, setCatalog] = useState<CatalogOffer[]>([]);
  const [offerId, setOfferId] = useState<number | "">("");

  useEffect(() => {
    api.offersCatalog().then(setCatalog);
  }, []);

  const available = useMemo(
    () => catalog.filter((o) => !existing.includes(o.id)),
    [catalog, existing]
  );

  const onAdd = async () => {
    if (offerId === "") return;
    await api.addOffer(streamId, Number(offerId));
    onDone();
  };

  return (
    <tr>
      <td colSpan={4}>
        <select
          value={offerId}
          onChange={(e) => setOfferId(e.target.value === "" ? "" : Number(e.target.value))}
        >
          <option value="">— выберите оффер —</option>
          {available.map((o) => (
            <option key={o.id} value={o.id}>{o.id} {o.name}</option>
          ))}
        </select>
        <button onClick={onAdd} disabled={offerId === ""}>Add</button>
        <button onClick={onCancel}>Cancel</button>
      </td>
    </tr>
  );
}
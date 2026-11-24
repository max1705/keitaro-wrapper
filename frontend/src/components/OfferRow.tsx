import type { OfferLink } from "../types";
import { api } from "../api/client";

interface Props {
  streamId: number;
  offer: OfferLink;
  onRefresh: () => void;
}

export function OfferRow({ streamId, offer, onRefresh }: Props) {
  const removed = offer.status === "removed";

  const onRemove = async () => {
    await api.removeOffer(streamId, offer.offer_id);
    onRefresh();
  };

  const onBringBack = async () => {
    await api.bringBack(streamId, offer.offer_id);
    onRefresh();
  };

  const onPin = async () => {
    await api.togglePin(streamId, offer.offer_id);
    onRefresh();
  };

  return (
    <tr className={removed ? "removed" : ""}>
      <td>
        {offer.offer_id} {offer.offer_name ?? ""}
      </td>
      <td>
        {/* Вес и кнопка пина рядом */}
        <span>{offer.share}%</span>
        {!removed && (
          <button
            className={`pin-btn ${offer.is_pinned ? "pinned" : ""}`}
            onClick={onPin}
            title={offer.is_pinned ? "Unpin" : "Pin"}
          >
            📌
          </button>
        )}
      </td>
      <td>{removed ? "removed" : "active"}</td>
      <td>
        {removed ? (
          <button onClick={onBringBack}>Bring back</button>
        ) : (
          <button onClick={onRemove}>Remove</button>
        )}
      </td>
    </tr>
  );
}
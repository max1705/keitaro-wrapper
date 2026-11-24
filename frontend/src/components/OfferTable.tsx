import { useState } from "react";
import type { Stream } from "../types";
import { OfferRow } from "./OfferRow";
import { AddOfferRow } from "./AddOfferRow";

interface Props {
  stream: Stream;
  onRefresh: () => void;
}

export function OfferTable({ stream, onRefresh }: Props) {
  const [showAdd, setShowAdd] = useState(false);

  return (
    <table className="offer-table">
      <thead>
        <tr>
          <th>Offer</th>
          <th>Share</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {stream.offers.map((o) => (
          <OfferRow
            key={o.id}
            streamId={stream.id}
            offer={o}
            onRefresh={onRefresh}
          />
        ))}
        {showAdd ? (
          <AddOfferRow
            streamId={stream.id}
            existing={stream.offers.map((o) => o.offer_id)}
            onDone={() => { setShowAdd(false); onRefresh(); }}
            onCancel={() => setShowAdd(false)}
          />
        ) : (
          <tr>
            <td colSpan={4}>
              <button onClick={() => setShowAdd(true)}>+ Add offer</button>
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
}
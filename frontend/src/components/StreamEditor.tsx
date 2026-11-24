import type { Stream } from "../types";
import { OfferTable } from "./OfferTable";
import { ActionBar } from "./ActionBar";

interface Props {
  stream: Stream;
  onRefresh: () => void;
}

export function StreamEditor({ stream, onRefresh }: Props) {
  const bg = stream.is_dirty ? "#fffbe6" : "#fff";

  return (
    <div className="stream" style={{ background: bg }}>
      <div className="stream-header">
        <strong>Stream: Flow {stream.position}</strong>
        <span>(#{stream.position})</span>
        {stream.is_dirty && <span className="dirty">не опубликован</span>}
      </div>

      {stream.has_offers && (
        <OfferTable stream={stream} onRefresh={onRefresh} />
      ) }

      {stream.has_offers && stream.is_dirty && (
        <ActionBar streamId={stream.id} onRefresh={onRefresh} />
      )}
    </div>
  );
}
import { api } from "../api/client";

interface Props {
  streamId: number;
  onRefresh: () => void;
}

export function ActionBar({ streamId, onRefresh }: Props) {
  const onPush = async () => {
    await api.push(streamId);
    onRefresh();
  };
  const onCancel = async () => {
    await api.cancel(streamId);
    onRefresh();
  };

  return (
    <div className="action-bar">
      <button onClick={onPush}>Push to KT</button>
      <button onClick={onCancel}>Cancel</button>
    </div>
  );
}
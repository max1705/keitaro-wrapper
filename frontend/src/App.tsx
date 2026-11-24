import { useEffect, useState } from "react";
import { api } from "./api/client";
import type { Campaign, Stream } from "./types";
import { StreamEditor } from "./components/StreamEditor";
import { CreateCampaignModal } from "./components/CreateCampaignModal";
import "./App.css";

function App() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [streams, setStreams] = useState<Stream[]>([]);
  const [loading, setLoading] = useState(false);
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  const loadCampaigns = async () => {
    await api.syncCampaigns();
    const list = await api.listCampaigns();
    setCampaigns(list);
    return list;
  };

  const loadStreams = async (cid: number) => {
    setLoading(true);
    try {
      const list = await api.getStreams(cid);
      // Сортируем: поток с офферами наверх
      const sorted = [...list].sort((a, b) => {
        if (a.has_offers === b.has_offers) return a.position - b.position;
        return a.has_offers ? -1 : 1;
      });
      setStreams(sorted);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { 
    loadCampaigns().then(list => {
      if (list.length && selected === null) setSelected(list[0].id);
    });
  }, []);

  useEffect(() => { 
    if (selected !== null) loadStreams(selected); 
  }, [selected]);

  const onFetch = async () => {
    if (selected === null) return;
    await api.fetchStreams(selected);
    await loadStreams(selected);
  };

  const onCampaignCreated = async (newCampaignId: number) => {
    const list = await loadCampaigns();
    // Автоматически выбираем только что созданную кампанию
    if (list.some(c => c.id === newCampaignId)) {
      setSelected(newCampaignId);
    }
  };

  return (
    <div className="app">
      <h1>Keitaro Wrapper</h1>
      
      <div className="toolbar">
        <select
          value={selected ?? ""}
          onChange={(e) => setSelected(Number(e.target.value))}
        >
          {campaigns.map((c) => (
            <option key={c.id} value={c.id}>{c.name} (#{c.id})</option>
          ))}
        </select>
        <button onClick={onFetch} disabled={selected === null}>Fetch Streams</button>
        
        <button onClick={() => setIsCreateOpen(true)} className="btn-primary">
          + Create Campaign
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {streams.map((s) => (
        <StreamEditor
          key={s.id}
          stream={s}
          onRefresh={() => selected !== null && loadStreams(selected)}
        />
      ))}

      {isCreateOpen && (
        <CreateCampaignModal 
          onClose={() => setIsCreateOpen(false)} 
          onCreated={onCampaignCreated} 
        />
      )}
    </div>
  );
}

export default App;
"use client";
import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api, Persona } from "./api";

type SessionState = {
  ready: boolean;
  device_id: string | null;
  persona: Persona;
  language: string;
  setPersona: (p: Persona) => Promise<void>;
  setLanguage: (l: string) => Promise<void>;
};

const SessionCtx = createContext<SessionState | null>(null);

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);
  const [device_id, setDevice] = useState<string | null>(null);
  const [persona, setPersonaState] = useState<Persona>("citizen");
  const [language, setLanguageState] = useState<string>("en");

  useEffect(() => {
    api.session()
      .then(s => {
        setDevice(s.device_id);
        setPersonaState(s.persona);
        setLanguageState(s.language_pref);
      })
      .finally(() => setReady(true));
  }, []);

  const setPersona = useCallback(async (p: Persona) => {
    setPersonaState(p);
    await api.setPersona(p);
  }, []);

  const setLanguage = useCallback(async (l: string) => {
    setLanguageState(l);
    await api.setLanguage(l);
  }, []);

  return (
    <SessionCtx.Provider value={{ ready, device_id, persona, language, setPersona, setLanguage }}>
      {children}
    </SessionCtx.Provider>
  );
}

export function useSession(): SessionState {
  const v = useContext(SessionCtx);
  if (!v) throw new Error("useSession must be inside SessionProvider");
  return v;
}

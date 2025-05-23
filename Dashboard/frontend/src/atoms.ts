import { atom } from "jotai";
import { Result } from "./models";

export const messageAtom = atom("");
export const isUploadedAtom = atom(false);
export const resultAtom = atom<Result | null>(null);

import { JSX } from 'react';
import { create } from 'zustand';

export interface IPopupStore {
    show: boolean;
    header?: string;
    text: string | JSX.Element;
    isSubmit?: boolean;
    confirmText?: string;
    dismissText?: string;
    onConfirm?: () => void;
    onDismiss?: () => void;
}

export interface IPopupState {
    show: boolean;
    header?: string;
    text: string | JSX.Element;
    isSubmit?: boolean;
    confirmText?: string;
    dismissText?: string;
    onConfirm: () => void;
    onDismiss: () => void;
    resetPopup: () => void;
}

const resetState = () => {
    return {
        show: false,
        header: "Alert",
        text: "",
        isSubmit: false,
        confirmText: "Yes",
        dismissText: "No",
        onConfirm: () => {},
    }
}

export const usePopupStore = create<IPopupState>((set) => {
    return {
        show: false,
        header: "Alert",
        isSubmit: false,
        text: "",
        confirmText: "Yes",
        dismissText: "No",
        onConfirm: () => set({show: false}),
        onDismiss: () => set(resetState()),
        resetPopup: () => set(resetState()),
    }
})
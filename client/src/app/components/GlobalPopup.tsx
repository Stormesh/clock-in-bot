"use client";

import React from "react";
import Popup from "./Popup";
import { usePopupStore } from "../zustand/popupStore";

const GlobalPopup = () => {
  const {
    show,
    header = "Alert",
    text,
    isSubmit = false,
    confirmText = "Yes",
    dismissText = "No",
    onConfirm = () => {},
    onDismiss = () => {},
  } = usePopupStore();

  return (
    <Popup
      show={show}
      header={header}
      text={text}
      isSubmit={isSubmit}
      confirmText={confirmText}
      dismissText={dismissText}
      onConfirm={onConfirm}
      onDismiss={onDismiss}
    />
  );
};

export default GlobalPopup;

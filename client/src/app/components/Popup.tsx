import React, { FC } from "react";
import PopupButton from "./PopupButton";
import { IPopupStore } from "../zustand/popupStore";

const Popup: FC<IPopupStore> = ({
  show,
  header = "Alert",
  text,
  isSubmit = false,
  confirmText = "Yes",
  dismissText = "No",
  onConfirm = () => {},
  onDismiss = () => {},
}) => {
  return (
    <div className={`alert-background ${show ? "flex" : "hidden"}`}>
      <div className={`alert-div ${show ? "scale-100" : "scale-0"}`}>
        <h1 className="alert-header">{header}</h1>
        {typeof text === "string" ? (
          <h3 className="mx-2 text-xl text-center">{text}</h3>
        ) : (
          text
        )}
        {!isSubmit && onConfirm && onDismiss && (
          <div>
            <PopupButton
              text={confirmText}
              onClick={onConfirm}
              isSubmit={isSubmit}
            />
            <PopupButton text={dismissText} onClick={onDismiss} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Popup;

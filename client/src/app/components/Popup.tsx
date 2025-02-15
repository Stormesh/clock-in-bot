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
    <div className={`w-full h-full bg-black/25 fixed z-10 top-0 left-0 transition-opacity justify-center items-center ${show ? "flex" : "hidden"}`}>
      <div className={`flex flex-col relative justify-center items-center border-2 rounded-xl border-[#8c7c97] bg-[#4f4357] min-h-32 min-w-28 max-w-[32rem] text-white transition-all ${show ? "scale-100" : "scale-0"}`}>
        <h1 className="text-4xl font-bold -mt-2 top-0 bg-[#8c7c97] rounded-t-lg w-full text-center">{header}</h1>
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

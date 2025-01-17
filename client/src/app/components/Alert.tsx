import React, { FC } from "react";
import AlertButton from "./AlertButton";

interface AlertProps {
  text: string;
  onConfirm: () => void;
  onDismiss: () => void;
  alert: {
    show: boolean;
    text: string;
    onConfirm: () => void;
  };
}

const Alert: FC<AlertProps> = ({ text, onConfirm, onDismiss, alert }) => {
  return (
    <div
      className={`w-full h-full bg-black bg-opacity-25 fixed z-10 top-0 left-0 transition-opacity justify-center items-center ${
        alert.show ? "flex" : "hidden"
      }`}
      aria-hidden={!alert.show}
    >
      <div className={`flex flex-col relative justify-center items-center border-2 rounded-xl border-[#8c7c97] bg-[#4f4357] min-h-36 min-w-28 max-w-[32rem] text-white z-10 transition-all ${
        alert.show ? "scale-100" : "scale-0"
      }`}>
        <h1 className="text-5xl font-bold top-0 bg-[#8c7c97] rounded-t-lg w-full text-center">
          Alert
        </h1>
        <h3 className="mx-2 text-2xl text-center">{text}</h3>
        <div>
          <AlertButton text="Yes" onClick={onConfirm} />
          <AlertButton text="No" onClick={onDismiss} />
        </div>
      </div>
    </div>
  );
};

export default Alert;

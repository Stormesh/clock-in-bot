import React, { FC } from "react";

interface AlertButtonProps {
  text: string;
  onClick: () => void;
}

const AlertButton: FC<AlertButtonProps> = ({ text, onClick }) => {
  return (
    <button
      className="bg-[#8c7c97] border-b-4 border-neutral-800 hover:bg-white hover:text-black text-xl rounded-lg px-4 py-2 m-2 hover:scale-110 transition-all duration-200 font-bold"
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default AlertButton;
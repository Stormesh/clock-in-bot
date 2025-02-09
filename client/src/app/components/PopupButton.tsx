import React, { FC } from "react";

interface IPopupButtonProps {
  text: string;
  isSubmit?: boolean;
  onClick?: () => void;
}

const PopupButton: FC<IPopupButtonProps> = ({ text, isSubmit = false, onClick }) => {
  return (
    <button
      type={isSubmit ? "submit" : "button"}
      className="bg-[#8c7c97] border-b-4 border-neutral-800 hover:bg-white hover:text-black text-xl rounded-lg px-4 py-2 m-2 hover:scale-110 transition-all duration-200 font-bold cursor-pointer"
      onClick={isSubmit ? undefined : onClick}
    >
      {text}
    </button>
  );
};

export default PopupButton;
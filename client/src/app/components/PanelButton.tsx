import Link from "next/link";
import React, { FC } from "react";

interface IPanelButtons {
  text: string;
  color: string;
  hoverColor: string;
  onClick?: () => void;
  isLink?: boolean;
  link?: string;
}

const PanelButton: FC<IPanelButtons> = ({
  text,
  color,
  hoverColor,
  isLink = false,
  link = "/",
  onClick,
}) => {
  return isLink ? (
    <Link
      href={link}
      className={`${color} mx-2 ${hoverColor} select-none hover:scale-110 transition-all duration-300 text-white font-bold py-2 px-4 rounded cursor-pointer`}
    >
      {text}
    </Link>
  ) : (
    <button
      className={`${color} mx-2 ${hoverColor} select-none hover:scale-110 transition-all duration-300 text-white font-bold py-2 px-4 rounded cursor-pointer`}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default PanelButton;

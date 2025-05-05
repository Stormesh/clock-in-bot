import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React, { FC } from "react";

interface SidebarButtonProps {
  text: string;
  icon: IconProp;
  onClick?: () => void;
  isLink?: boolean;
  link?: string;
}

const SidebarDesign: FC<SidebarButtonProps> = ({ icon, text, onClick }) => {
  return (
    <div className="select-none cursor-pointer px-5 py-1 w-[100%] dark:text-white text-black dark:hover:bg-white/10 hover:bg-black/10" onClick={onClick}>
        <FontAwesomeIcon
          icon={icon}
          style={{ width: "18px", height: "18px" }}
          className="inline-block dark:text-white text-gray-800 mr-3"
        />
        <span className="text-lg font-medium">{text}</span>
    </div>
  );
};

const SidebarButton: FC<SidebarButtonProps> = ({
  icon,
  text,
  isLink,
  link,
  onClick,
}) => {
  return isLink ? (
    <Link href={"/" + link}>
      <SidebarDesign icon={icon} text={text} />
    </Link>
  ) : (
    <SidebarDesign icon={icon} text={text} onClick={onClick} />
  );
};

export default SidebarButton;

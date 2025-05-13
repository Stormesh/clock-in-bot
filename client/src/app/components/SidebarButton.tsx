import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React from "react";

interface SidebarButtonProps {
  text: string;
  icon: IconProp;
  onClick?: () => void;
  href?: string;
}

const SidebarButton = ({ icon, text, onClick, href }: SidebarButtonProps) => {
  const content = (
    <>
      <FontAwesomeIcon
        icon={icon}
        style={{ width: "18px", height: "18px" }}
        className="inline-block dark:text-white text-gray-800 mr-3"
      />
      <span className="text-lg font-medium">{text}</span>
    </>
  );

  const commonClasses = "cursor-pointer inline-block select-none px-5 py-1 w-[100%] dark:text-white text-black dark:hover:bg-white/10 hover:bg-black/10";

  if (href) {
    return (
      <Link href={href} className={commonClasses}>
        {content}
      </Link>
    );
  }

  return (
    <div className={commonClasses} onClick={onClick}>
      {content}
    </div>
  );
};

export default SidebarButton;

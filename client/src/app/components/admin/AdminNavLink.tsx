"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import React, { FC } from "react";

interface IAdminNavLinkProps {
  href: string;
  text: string;
}

const AdminNavLink: FC<IAdminNavLinkProps> = ({ href, text }) => {
  const path = usePathname();

  return (
    <Link
      className={`font-bold p-2 border-b-3 transition-all duration-300 text-white ${
        path === href ? "underline border-purple-300" : "border-transparent hover:border-purple-300"
      }`}
      href={href}
    >
      {text}
    </Link>
  );
};

export default AdminNavLink;

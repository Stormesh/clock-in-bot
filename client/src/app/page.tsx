import ClockList from "./components/ClockList";
import { auth } from "../auth";
import Warning from "./components/Warning";
import GlobalPopup from "./components/GlobalPopup";
import { SessionProvider } from "next-auth/react";

export default async function Home() {
  const session = await auth();

  if (!session) {
    return (
      <Warning
        text="You must be logged in to view this page."
        link="/login"
        linkText="Login"
      />
    );
  }

  return (
    <>
      <GlobalPopup />
      <SessionProvider>
        <ClockList />
      </SessionProvider>
    </>
  );
}

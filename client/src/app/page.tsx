import ClockList from "./components/ClockList";
import { auth } from "../auth";
import Warning from "./components/Warning";
import UserPanel from "./components/UserPanel";
import GlobalPopup from "./components/GlobalPopup";

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
      <UserPanel />
      <GlobalPopup />
      <ClockList />
    </>
  );
}

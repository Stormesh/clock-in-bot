export enum Action {
  LogIn = "Login",
  LogOut = "Logout",
  Create = "Create",
  Update = "Update",
  Delete = "Delete",
}

export enum Severity {
  Low = "Info",
  Medium = "Warning",
  High = "Danger",
}

export enum Permissions {
  SignUp = "sign-up",
  Delete = "delete-user",
  Update = "update-user",
  Logs = "view-logs",
  Warn = "warn-agent",
  Kick = "kick-agent"
}

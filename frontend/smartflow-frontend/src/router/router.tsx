import { createBrowserRouter } from "react-router-dom";

import HomePage from "../pages/HomePage";
import ArticlePage from "../pages/ArticlePage";
import EditorPage from "../pages/EditorPage";
import LoginPage from "../pages/LoginPage";
import RegisterPage from "../pages/RegisterPage";
import ProfilePage from "../pages/ProfilePage";
import NotificationsPage from "../pages/NotificationsPage";
import SearchPage from "../pages/SearchPage";

export const router = createBrowserRouter([
  { path: "/", element: <HomePage /> },
  { path: "/article/:slug", element: <ArticlePage /> },
  { path: "/editor", element: <EditorPage /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },
  { path: "/profile/:username", element: <ProfilePage /> },
  { path: "/notifications", element: <NotificationsPage /> },
  { path: "/search", element: <SearchPage /> },
]);
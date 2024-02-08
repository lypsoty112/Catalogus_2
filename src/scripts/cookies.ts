// cookie_utils.ts

// For browser environment (commonJS)
declare global {
    interface Document {
      cookie: string;
    }
  }
  
  // For Node.js environment (module.exports)
  export interface CookieOptions {
    expires?: Date;
    path?: string;
  }
  
  function getCookieImpl(name: string): string | null {
    if (typeof document !== 'undefined') {
      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const parts = cookie.trim().split('=');
        if (parts.length === 2 && parts[0] === name) {
          return parts[1];
        }
      }
    }
    return null;
  }
  
  export function getCookie(name: string): string | null {
    return getCookieImpl(name);
  }
  
  function setCookieImpl(name: string, value: string, options?: CookieOptions) {
    if (typeof document !== 'undefined') {
      let cookieStr = `${name}=${value}`;
      if (options) {
        if (options.expires) {
          cookieStr += `; expires=${options.expires.toUTCString()}`;
        }
        if (options.path) {
          cookieStr += `; path=${options.path}`;
        }
      }
      document.cookie = cookieStr;
    }
  }
  
  export function setCookie(name: string, value: string, options?: CookieOptions) {
    setCookieImpl(name, value, options);
  }
  
  function deleteCookieImpl(name: string) {
    if (typeof document !== 'undefined') {
      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
    }
  }
  
  export function deleteCookie(name: string) {
    deleteCookieImpl(name);
  }
  
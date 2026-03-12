export function useApi() {
  const request = async () => {
    console.log("API request");
  };

  return { request };
}
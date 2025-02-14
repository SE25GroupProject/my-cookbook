import { useDebounceFn, useMount } from 'ahooks'

export function useFixScroll(hasMore: boolean, fetchMore: () => void) {
  // debounce is necessary
  const fixFetch = useDebounceFn(
    () => {
      const firstLoaderItem = document.querySelector('.loader-item')
      const scrollContainer = document.querySelector('.scroll-container')
      if (!firstLoaderItem || !scrollContainer) {
        return
      }
      if (
        // only when user do not scroll content
        // The loading will continue only when the loader element appears on the scroll-container.
        scrollContainer.scrollTop === 0 &&
        firstLoaderItem.getBoundingClientRect().top <
          scrollContainer.getBoundingClientRect().bottom
      ) {
        // console.log("fixed");
        fetchMore()
      }
    },
    {
      wait: 500,
    }
  )
  // useMount equals useEffect(()=>{doSomething();},[]);
  useMount(() => {
    const observer = new MutationObserver((mutationsList) => {
      for (let mutation of mutationsList) {
        if (mutation.type === 'childList') {
          // console.log("Child nodes have been added or removed.");
          fixFetch.run()
        }
      }
    })

    if (!hasMore) {
      return
    }
    // scroll-items-container is the container for the items.
    const targetNode = document.getElementById('scroll-items-container')
    if (!targetNode) {
      return
    }

    const config = { childList: true, subtree: false }
    // console.log("start observe");
    observer.observe(targetNode, config)
    return () => {
      observer.disconnect()
    }
  })
}

// @ts-ignore
import bilingualScript from "./scripts/bilingual.inline"
import { QuartzComponent, QuartzComponentConstructor } from "./types"

const Bilingual: QuartzComponent = () => {
  return (
    <button id="bilingual-toggle" class="bilingual-toggle" aria-label="Toggle Chinese translation" aria-pressed="false" title="Show Chinese translation">
      中
    </button>
  )
}

Bilingual.afterDOMLoaded = bilingualScript

export default (() => Bilingual) satisfies QuartzComponentConstructor

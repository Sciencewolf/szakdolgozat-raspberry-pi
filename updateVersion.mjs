import { createClient } from "@supabase/supabase-js"
import * as process from "node:process";

async function run() {
    const supabase = createClient(
        process.env.URL.toString(),
        process.env.KEY.toString()
    );

    if (process.argv.length <= 2) {
        console.log("no version provided")
        return
    }

    const { error } = await supabase.from('version')
        .update({v: process.argv[2]})
        .eq('id', 1)

    if (error) {
        console.error(error)
    }
}

await run()

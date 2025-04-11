import {genkit} from 'genkit';
import {googleAI} from '@genkit-ai/googleai';

export const ai = genkit({
  promptDir: './prompts',
  plugins: [
    googleAI({
      apiKey: 'AIzaSyD9d0kiIo8ms4ItQI_hfowhqR7gjbN5kfI',
    }),
  ],
  model: 'googleai/gemini-2.0-flash',
});

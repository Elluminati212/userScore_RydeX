'use server';
/**
 * @fileOverview Dynamic pricing engine AI agent.
 *
 * - adjustPricing - A function that handles the dynamic pricing adjustment process.
 * - AdjustPricingInput - The input type for the adjustPricing function.
 * - AdjustPricingOutput - The return type for the adjustPricing function.
 */

import {ai} from '@/ai/ai-instance';
import {z} from 'genkit';

const AdjustPricingInputSchema = z.object({
  timeOfDay: z.string().describe('The time of day when the trip occurred.'),
  dayOfWeek: z.string().describe('The day of the week when the trip occurred.'),
  location: z.string().describe('The location where the trip started.'),
  demand: z.number().describe('The current demand for trips.'),
  historicalDemand: z.number().describe('The historical demand for trips at this time and location.'),
});
export type AdjustPricingInput = z.infer<typeof AdjustPricingInputSchema>;

const AdjustPricingOutputSchema = z.object({
  surgeMultiplier: z.number().describe('The recommended surge pricing multiplier.'),
  reason: z.string().describe('The reason for the surge pricing adjustment.'),
});
export type AdjustPricingOutput = z.infer<typeof AdjustPricingOutputSchema>;

export async function adjustPricing(input: AdjustPricingInput): Promise<AdjustPricingOutput> {
  return adjustPricingFlow(input);
}

const prompt = ai.definePrompt({
  name: 'adjustPricingPrompt',
  input: {
    schema: z.object({
      timeOfDay: z.string().describe('The time of day when the trip occurred.'),
      dayOfWeek: z.string().describe('The day of the week when the trip occurred.'),
      location: z.string().describe('The location where the trip started.'),
      demand: z.number().describe('The current demand for trips.'),
      historicalDemand: z.number().describe('The historical demand for trips at this time and location.'),
    }),
  },
  output: {
    schema: z.object({
      surgeMultiplier: z.number().describe('The recommended surge pricing multiplier.'),
      reason: z.string().describe('The reason for the surge pricing adjustment.'),
    }),
  },
  prompt: `You are a pricing expert for a ridesharing company. Your goal is to dynamically adjust pricing based on real-time trip demand and predicted surge events.

Consider the following factors:
- Time of day: {{{timeOfDay}}}
- Day of week: {{{dayOfWeek}}}
- Location: {{{location}}}
- Current demand: {{{demand}}}
- Historical demand: {{{historicalDemand}}}

Based on these factors, determine the appropriate surge pricing multiplier. Explain the reasoning for your adjustment.

Output the surgeMultiplier as a floating point number.  Output the reason as a string.
`,
});

const adjustPricingFlow = ai.defineFlow<
  typeof AdjustPricingInputSchema,
  typeof AdjustPricingOutputSchema
>({
  name: 'adjustPricingFlow',
  inputSchema: AdjustPricingInputSchema,
  outputSchema: AdjustPricingOutputSchema,
}, async input => {
  const {output} = await prompt(input);
  return output!;
});

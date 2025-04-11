// analyze-surge-patterns.ts
'use server';

/**
 * @fileOverview Analyzes historical trip data to identify surge patterns.
 *
 * - analyzeSurgePatterns - A function that triggers the surge pattern analysis.
 * - AnalyzeSurgePatternsInput - The input type for the analyzeSurgePatterns function.
 * - AnalyzeSurgePatternsOutput - The return type for the analyzeSurgePatterns function.
 */

import {ai} from '@/ai/ai-instance';
import {z} from 'genkit';
import {getTrips, Trip} from '@/services/mongodb';

const AnalyzeSurgePatternsInputSchema = z.object({
  timeOfDayWeight: z.number().default(1).describe('Weight for time of day in surge analysis.'),
  dayOfWeekWeight: z.number().default(1).describe('Weight for day of week in surge analysis.'),
  locationWeight: z.number().default(1).describe('Weight for location in surge analysis.'),
  demandWeight: z.number().default(1).describe('Weight for demand in surge analysis.'),
});
export type AnalyzeSurgePatternsInput = z.infer<typeof AnalyzeSurgePatternsInputSchema>;

const AnalyzeSurgePatternsOutputSchema = z.object({
  surgePatterns: z.string().describe('Detailed analysis of surge patterns.'),
  optimalPricingStrategy: z.string().describe('Recommended pricing strategies based on surge analysis.'),
});
export type AnalyzeSurgePatternsOutput = z.infer<typeof AnalyzeSurgePatternsOutputSchema>;

export async function analyzeSurgePatterns(input: AnalyzeSurgePatternsInput): Promise<AnalyzeSurgePatternsOutput> {
  return analyzeSurgePatternsFlow(input);
}

const analyzeSurgePatternsPrompt = ai.definePrompt({
  name: 'analyzeSurgePatternsPrompt',
  input: {
    schema: z.object({
      tripData: z.string().describe('Historical trip data in JSON format.'),
      timeOfDayWeight: z.number().describe('Weight for time of day in surge analysis.'),
      dayOfWeekWeight: z.number().describe('Weight for day of week in surge analysis.'),
      locationWeight: z.number().describe('Weight for location in surge analysis.'),
      demandWeight: z.number().describe('Weight for demand in surge analysis.'),
    }),
  },
  output: {
    schema: z.object({
      surgePatterns: z.string().describe('Detailed analysis of surge patterns.'),
      optimalPricingStrategy: z.string().describe('Recommended pricing strategies based on surge analysis.'),
    }),
  },
  prompt: `You are an expert in analyzing trip data to identify surge patterns and recommend optimal pricing strategies.

Analyze the following historical trip data to identify factors that contribute to surge events, considering the weights for time of day ({{{timeOfDayWeight}}}), day of week ({{{dayOfWeekWeight}}}), location ({{{locationWeight}}}), and demand ({{{demandWeight}}}).

Trip Data:
{{{tripData}}}

Consider the trip start time, trip end time, source and destination locations, total distance, total time, and payment status to analyze surge patterns.

Based on your analysis, provide a detailed description of the surge patterns and suggest an optimal pricing strategy.

Format the surgePatterns and optimalPricingStrategy to be human-readable.
`,
});

const analyzeSurgePatternsFlow = ai.defineFlow<
  typeof AnalyzeSurgePatternsInputSchema,
  typeof AnalyzeSurgePatternsOutputSchema
>(
  {
    name: 'analyzeSurgePatternsFlow',
    inputSchema: AnalyzeSurgePatternsInputSchema,
    outputSchema: AnalyzeSurgePatternsOutputSchema,
  },
  async input => {
    const trips: Trip[] = await getTrips();
    const tripData = JSON.stringify(trips);

    const {output} = await analyzeSurgePatternsPrompt({
      ...input,
      tripData,
    });
    return output!;
  }
);

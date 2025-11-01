/**
 * Health check endpoint for Docker healthcheck and monitoring
 */
export async function GET() {
  return Response.json(
    {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'confradar-web',
    },
    { status: 200 }
  );
}

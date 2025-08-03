"""CLI interface - mirrors bustcall/src/cli/main.rs"""

import click
import asyncio
from ..core.config import BustcallConfig, PolyCallConfig
from ..servers.server import PyBustcallServer
from ..delegation import DelegationManager

@click.group()
def cli():
    """PyBustcall - Python binding for OBINexus Bustcall"""
    pass

@cli.command()
@click.option('--port', default=8084, help='Server port')
@click.option('--config', help='PolyCall configuration file')
def serve(port: int, config: str):
    """Start PyBustcall server"""
    
    # Load configuration
    bustcall_config = BustcallConfig(daemon_port=3000)
    if config:
        polycall_config = PolyCallConfig.from_polycallfile(config)
        bustcall_config.polycall_config = polycall_config
    
    # Start server
    server = PyBustcallServer(bustcall_config)
    server.run(port=port)

@cli.command()
@click.argument('target')
@click.option('--strategy', default='dimensional', help='Cache bust strategy')
@click.option('--binding', default='auto', help='Target binding')
def bust(target: str, strategy: str, binding: str):
    """Execute cache bust operation"""
    
    async def _bust():
        config = BustcallConfig()
        delegation_manager = DelegationManager(config)
        result = await delegation_manager.execute_bust(target, strategy, 6)
        click.echo(f"Cache bust result: {result}")
    
    asyncio.run(_bust())

@cli.command()
def status():
    """Show PyBustcall status"""
    # Implementation for status command
    pass

if __name__ == '__main__':
    cli()
